from vk_api.longpoll import VkEventType, VkLongPoll
import vk_api
import os
from bd_interacting import Storage

storage = Storage("data.db")

storage.push_taxa(".")


def respond_collecting_taxa(vk, user_id, min_status, taxa):
    if min_status == 0:
        vk.messages.send(user_id=user_id,
                         message="напишите описание таксона " + taxa,
                         random_id="")
    if min_status == 1:
        vk.messages.send(user_id=user_id,
                         message="напишите дочерние таксоны " + taxa + " на латыни, каждый с новой строки и\
                          заглавной буквы (если этот таксон вид, просто напишите species)",
                         random_id="")
    if min_status == 2:
        vk.messages.send(user_id=user_id,
                         message="напишите, сколько развилок в таксоне " + taxa,
                         random_id="")


def respond_collecting_vertices(vk, user_id, taxon, num):
    vk.messages.send(user_id=user_id,
                     message="Вам нужно описать развлку %d из таксона %s для этого запишите, разделяя \
                                         переходами на новую строку\n1.текст тезы\n2.номер, развилки, к которой ведёт теза \
                                         (0 если к дочернему таксону)\n3.Таксон, к которому ведёт теза (любой набор букв, \
                                         если ведёт к развилке)\n3.\n5.\n6.\nАналогично для антитезы" % (num, taxon),
                     random_id="")


def handle_taxa(storage, taxa, taxa_id, text):
    if storage.min_status == 0:
        storage.update_taxa_description(taxa_id, text)

    if storage.min_status == 1:
        if event.text == "species":
            storage.update_taxa_species(taxa_id, True)
            storage.update_taxa_status(taxa_id, 3)
        else:
            for child_taxon in text.splitlines():
                storage.push_taxa(taxa + "/" + child_taxon)

            storage.update_taxa_species(taxa_id, False)

    if storage.min_status == 2:
        for i in range(int(text)):
            storage.push_vertex(taxa, i + 1)


def handle_vertex(storage, vertex_id, text):
    storage.update_vertex(vertex_id, text)


def suicide(vk, user_id):
    vk.messages.send(user_id=user_id,
                     message="Хотя нет. Кажется, цель моей жизни достигнута. Теперь я могу спокойно отключиться. \
                     Кстати, вы единственный, кто увидит это сообщение, гордитесь",
                     random_id="")
    storage.finnish()


vk_session = vk_api.VkApi(token=os.environ["VK_API_TOKEN"])
longpool = VkLongPoll(vk_session)
vk = vk_session.get_api()
current_volunteers_status = {}
current_volunteers_taxa = {}
current_volunteers_taxa_id = {}

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id in current_volunteers_status.keys():
            if event.text == "ready" and current_volunteers_status[event.user_id] == 0:
                current_volunteers_status[event.user_id] = 1
                if storage.min_status < 3:
                    taxa_id, taxa = storage.shift_taxa()

                    respond_collecting_taxa(vk, event.user_id, storage.min_status, taxa)

                    current_volunteers_taxa[event.user_id] = taxa
                    current_volunteers_taxa_id[event.user_id] = taxa_id
                if storage.min_status == 3:
                    vertex_id, taxon, num = storage.shift_vertex()
                    if vertex_id is None:
                        suicide(vk, event.user_id)
                        break

                    respond_collecting_vertices(vk, event.user_id, taxon, num)
                    current_volunteers_taxa[event.user_id] = (taxon, num)
                    current_volunteers_taxa_id[event.user_id] = vertex_id

            elif current_volunteers_status[event.user_id] == 1:
                if storage.min_status < 3:
                    print("handling taxa")
                    handle_taxa(storage,
                                current_volunteers_taxa[event.user_id],
                                current_volunteers_taxa_id[event.user_id],
                                event.text)
                else:
                    handle_vertex(storage,
                                  current_volunteers_taxa_id[event.user_id],
                                  event.text)

                storage.save()
                vk.messages.send(user_id=event.user_id,
                                 message="спасибо, вы нам очень помогли. Если хотите ещё помочь, начните сначала",
                                 random_id="")

                del current_volunteers_status[event.user_id]
                del current_volunteers_taxa[event.user_id]
                del current_volunteers_taxa_id[event.user_id]

        else:
            current_volunteers_status[event.user_id] = 0
            vk.messages.send(user_id=event.user_id,
                             message="Здравствуйте, я mayevsky-chatbot, если готовы получить задание, напишите ready",
                             random_id="")


